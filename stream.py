import streamlit as st
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from litellm import completion

# --- Configuration and Initialization ---
# You might want to move these to a separate config file or Streamlit secrets
urls = " "
api_keys = "bow bow"
pdf_file = "tnesevai_services.pdf"

@st.cache_resource
def initialize_rag_system():
    """Initializes and caches the RAG components."""
    try:
        st.write("Initializing RAG system...")
        embeddings = OllamaEmbeddings(model="qwen3:latest")
        st.write("Loading PDF document...")
        loader = PyPDFLoader(pdf_file)
        docs = loader.load()
        st.write(f"📄 Loaded {len(docs)} documents.")
        
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=200)
        chunks = text_splitter.split_documents(docs)
        st.write(f"✂️ Split into {len(chunks)} chunks.")

        client = QdrantClient(url=urls, api_key=api_keys)
        
        collection_exists = False
        try:
            client.get_collection("tnesevai")
            collection_exists = True
        except Exception:
            pass

        if not collection_exists:
            st.write("🔄 Creating and populating a new collection...")
            client.recreate_collection(
                collection_name="tnesevai",
                vectors_config={"size": 1024, "distance": "Cosine"}
            )
            store = QdrantVectorStore(
                client=client,
                collection_name="tnesevai",
                embedding=embeddings,
            )
            store.add_documents(chunks)
            st.write("✅ Collection populated.")
        else:
            st.write("✅ Collection 'tnesevai' already exists. Connecting to it.")
            store = QdrantVectorStore.from_existing_collection(
                collection_name="tnesevai",
                url=urls,
                api_key=api_keys,
                # prefer_grpc=True,
                embedding=embeddings,
            )
        return store
    except Exception as e:
        st.error(f"❌ An error occurred during initialization: {e}")
        st.stop()

# --- Streamlit UI Components ---
st.title("🏛️ TNesevai Chatbot")
st.markdown("Ask questions about Tamil Nadu's Government Services.")

# Initialize the RAG system and store it in a session state
if 'store' not in st.session_state:
    st.session_state.store = initialize_rag_system()

store = st.session_state.store

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Main conversation loop
if prompt := st.chat_input("Ask a question about TN services:"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        try:
            # Search for relevant chunks based on user input
            with st.spinner("🔍 Searching for relevant information..."):
               chunks = store.similarity_search(prompt, k=3)
          # 🔎 DEBUG: Show Retrieved Chunks
            if len(chunks) == 0:
                    st.warning("❌ No relevant chunks found from the PDF. RAG might not be working.")
                    st.stop()
            else:
                    st.subheader("📚 Retrieved Context (Debug View)")
                    for i, c in enumerate(chunks):
                        st.write(f"### Chunk {i+1}")
                        st.write(c.page_content[:500])  # show first part of chunk
                        st.write("---")
     
                    

            # Combine chunks for RAG
            rag_context = "\n\n".join([chunk.page_content for chunk in chunks])

            # Generate response using litellm
            messages = [{
                "content": f"Based on the following context about Tamil Nadu government services, answer the question: {prompt}\n\nContext: {rag_context}",
                "role": "user"
            }]

            with st.spinner("🤖 Generating answer..."):
                response = completion(
                    model="ollama/qwen3:latest",
                    messages=messages,
                    api_base="http://localhost:11434",
                    stream=True
                )
                
                # Stream the response
                for part in response:
                    full_response += part.choices[0].delta.content or ""
                    message_placeholder.markdown(full_response + "▌")
                message_placeholder.markdown(full_response)
        
        except Exception as e:
            st.error(f"❌ An error occurred: {e}")
            st.warning("Make sure Ollama is running and the 'qwen3:0.6b' model is available.")
            full_response = "An error occurred during generation."

    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": full_response})
