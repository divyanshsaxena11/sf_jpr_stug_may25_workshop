import streamlit as st
import json
import _snowflake
from snowflake.snowpark.context import get_active_session

session = get_active_session()

API_ENDPOINT = "/api/v2/cortex/agent:run"
API_TIMEOUT = 50000  # in milliseconds

CORTEX_SEARCH_SERVICES = (
    "hospital_challenges_tutorial_db.PUBLIC.STUDY_GUIDE_SEARCH_SERVICE"
)
SEMANTIC_MODELS = (
    "@hospital_challenges_tutorial_db.public.landing_stg/patient_report.yaml"
)


def run_snowflake_query(query):
    try:
        df = session.sql(query.replace(";", ""))

        return df

    except Exception as e:
        st.error(f"Error executing SQL: {str(e)}")
        return None, None


def snowflake_api_call(query: str, limit: int = 10):

    payload = {
        "model": "claude-3-5-sonnet",
        "response-instruction": "You will always maintain a serious tone and provide a concise response, you will always refer the user as Doctor.",
        "messages": [{"role": "user", "content": [{"type": "text", "text": query}]}],
        "tools": [
            {"tool_spec": {"type": "cortex_analyst_text_to_sql", "name": "analyst1"}},
            {"tool_spec": {"type": "cortex_search", "name": "search1"}},
        ],
        "tool_resources": {
            "analyst1": {"semantic_model_file": SEMANTIC_MODELS},
            "search1": {
                "name": CORTEX_SEARCH_SERVICES,
                "max_results": limit,
                "id_column": "CHUNK",
            },
        },
    }

    try:
        resp = _snowflake.send_snow_api_request(
            "POST",  # method
            API_ENDPOINT,  # path
            {},  # headers
            {},  # params
            payload,  # body
            None,  # request_guid
            API_TIMEOUT,  # timeout in milliseconds,
        )

        if resp["status"] != 200:
            st.error(
                f"❌ HTTP Error: {resp['status']} - {resp.get('reason', 'Unknown reason')}"
            )
            st.error(f"Response details: {resp}")
            return None

        try:
            response_content = json.loads(resp["content"])
        except json.JSONDecodeError:
            st.error(
                "❌ Failed to parse API response. The server may have returned an invalid JSON format."
            )
            st.error(f"Raw response: {resp['content'][:200]}...")
            return None

        return response_content

    except Exception as e:
        st.error(f"Error making request: {str(e)}")
        return None


def process_sse_response(response):
    """Process SSE response"""
    text = ""
    sql = ""
    citations = []

    if not response:
        return text, sql, citations
    if isinstance(response, str):
        return text, sql, citations
    try:
        for event in response:
            if event.get("event") == "message.delta":
                data = event.get("data", {})
                delta = data.get("delta", {})

                for content_item in delta.get("content", []):
                    content_type = content_item.get("type")
                    if content_type == "tool_results":
                        tool_results = content_item.get("tool_results", {})
                        if "content" in tool_results:
                            for result in tool_results["content"]:
                                if result.get("type") == "json":
                                    text += result.get("json", {}).get("text", "")
                                    search_results = result.get("json", {}).get(
                                        "searchResults", []
                                    )
                                    for search_result in search_results:
                                        citations.append(
                                            {
                                                "source_id": search_result.get(
                                                    "source_id", ""
                                                ),
                                                "doc_id": search_result.get(
                                                    "doc_id", ""
                                                ),
                                            }
                                        )
                                    sql = result.get("json", {}).get("sql", "")
                    if content_type == "text":
                        text += content_item.get("text", "")

    except json.JSONDecodeError as e:
        st.error(f"Error processing events: {str(e)}")

    except Exception as e:
        st.error(f"Error processing events: {str(e)}")

    return text, sql, citations


def main():
    st.title("Doctor's Cortex Assistant")

    # Sidebar for new chat
    with st.sidebar:
        if st.button("New Conversation", key="new_chat"):
            st.session_state.messages = [
                {
                    "role": "assistant",
                    "content": "Good Day Doctor, How can I help today?",
                }
            ]
            st.rerun()

    # Initialize session state
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "Good Day Doctor, How can I help today?"}
        ]

    for message in st.session_state.messages:
        my_avater = "🥼" if message["role"] == "user" else "🤖"
        with st.chat_message(message["role"], avatar=my_avater):
            st.markdown(message["content"].replace("•", "\n\n"))

    if query := st.chat_input("How can I help you with your request?"):
        # Add user message to chat
        with st.chat_message("user", avatar="🥼"):
            st.markdown(query)
        st.session_state.messages.append({"role": "user", "content": query})

        # Get response from API
        with st.spinner("Processing your request..."):
            response = snowflake_api_call(query, 4)
            text, sql, citations = process_sse_response(response)

            # Add assistant response to chat
            if text:
                text = text.replace("【†1†】", "")
                st.session_state.messages.append({"role": "assistant", "content": text})

                with st.chat_message("assistant", avatar="🤖"):
                    st.markdown(text.replace("•", "\n\n"))
                    if citations:
                        #                        st.write(citations)
                        st.header("Hospital's Internal Study Library (Archives):")
                        for citation in citations:
                            patient_id = citation.get("doc_id", "")
                            if patient_id:
                                st.write(patient_id)
            #                                query = f"SELECT * FROM hospital_challenges_tutorial_db.PUBLIC.CHUNK_PARSED_INVOICES WHERE chunk ilike '%{patient_id}%'"
            #                                result = run_snowflake_query(query)
            #                                result_df = result.to_pandas()
            #                                st.write(result_df)

            # Display SQL if present
            if sql:
                with st.chat_message("assistant", avatar="🤖"):
                    st.markdown("### Snowflake SQL for Report")
                    st.code(sql, language="sql")
                    sql_results = run_snowflake_query(sql)
                    if sql_results:
                        st.write("### Requested Report")
                        st.dataframe(sql_results)


if __name__ == "__main__":
    main()
