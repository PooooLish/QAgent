import streamlit as st
import tempfile
from rag.ingest import load_document_text, chunk_text
from agent.workflow import GeneralQAAgent
from agent.memory import Memory

import re

def render_mixed_answer(answer: str):
    # 先处理块公式 \[ ... \]
    block_formulas = re.findall(r"\\\[(.*?)\\\]", answer, flags=re.DOTALL)
    if block_formulas:
        text = re.sub(r"\\\[(.*?)\\\]", "", answer, flags=re.DOTALL).strip()
        if text:
            st.write(text)

        for formula in block_formulas:
            st.latex(formula.strip())
    else:
        st.write(answer)

st.set_page_config(page_title="General QA Agent", page_icon="🤖", layout="wide")

st.title("🤖 General QA Agent")
st.caption("支持普通问答、文档问答、总结、提纲生成和简单计算。")

if "messages" not in st.session_state:
    st.session_state.messages = []

if "chunks" not in st.session_state:
    st.session_state.chunks = []

if "doc_name" not in st.session_state:
    st.session_state.doc_name = None

if "memory" not in st.session_state:
    st.session_state.memory = Memory(max_turns=8)

if "agent" not in st.session_state:
    st.session_state.agent = GeneralQAAgent(model="gpt-4o-mini")

uploaded_file = st.file_uploader("上传文档（目前支持 PDF / TXT / MD）", type=["pdf", "txt", "md"])

if uploaded_file is not None:
    if st.session_state.doc_name != uploaded_file.name:
        suffix = "." + uploaded_file.name.split(".")[-1].lower()

        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp_file:
            tmp_file.write(uploaded_file.read())
            tmp_path = tmp_file.name

        text = load_document_text(tmp_path)

        if not text.strip():
            st.error("无法从文件中提取文本。")
            st.stop()

        chunks = chunk_text(text, chunk_size=800, overlap=120)

        st.session_state.chunks = chunks
        st.session_state.doc_name = uploaded_file.name
        st.session_state.messages = []
        st.session_state.memory = Memory(max_turns=8)

        st.success(f"已加载文档：{uploaded_file.name}")
        st.info(f"共切分为 {len(chunks)} 个文本片段。")

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

query = st.chat_input("请输入你的问题")

if query:
    st.session_state.messages.append({"role": "user", "content": query})
    st.session_state.memory.add("user", query)

    with st.chat_message("user"):
        st.markdown(query)

    with st.chat_message("assistant"):
        with st.spinner("思考中..."):
            result = st.session_state.agent.run(
                query=query,
                chunks=st.session_state.chunks,
                memory=st.session_state.memory,
            )

            answer = result["answer"]
            render_mixed_answer(answer)

        with st.expander("查看系统细节"):
            st.write("route =", result["route"])
            st.write("retrieval_mode =", result.get("retrieval_mode", "none"))
            if result.get("retrieved_chunks"):
                for i, chunk in enumerate(result["retrieved_chunks"], 1):
                    st.markdown(f"**Chunk {i}:**")
                    st.write(chunk)

    st.session_state.messages.append({"role": "assistant", "content": answer})
    st.session_state.memory.add("assistant", answer)