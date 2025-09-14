install python 3.11 +
enable wsl2 for windows
install docker for windows
update your nvidia drivers and cuda drivers
get the free n8n license key

pruning docker volumes: docker volume prune


once n8n is installed
	activate your free n8n license key
	go to community nodes section and download the nodes:
		n8n-nodes-lightrag
		n8n-nodes-query-retriever-rerank
			AI->Other AI nodes->Tools->n8n-nodes-query-retriever-rerank
			
LightRAG is effective, and it makes really pretty graphs, but it takes a looong time


This works in postgres
https://supabase.com/docs/guides/ai/langchain?queryGroups=database-method&database-method=sql

-- Enable the pgvector extension to work with embedding vectors
CREATE EXTENSION IF NOT EXISTS vector;

-- Create a table to store your documents
create table documents (
  id bigserial primary key,
  content text, -- corresponds to Document.pageContent
  metadata jsonb, -- corresponds to Document.metadata
  embedding vector(1536) -- 1536 works for OpenAI embeddings, change if needed
);

-- Create a function to search for documents
create function match_documents (
  query_embedding vector(1536),
  match_count int default null,
  filter jsonb DEFAULT '{}'
) returns table (
  id bigint,
  content text,
  metadata jsonb,
  similarity float
)
language plpgsql
as $$
#variable_conflict use_column
begin
  return query
  select
    id,
    content,
    metadata,
    1 - (documents.embedding <=> query_embedding) as similarity
  from documents
  where metadata @> filter
  order by documents.embedding <=> query_embedding
  limit match_count;
end;
$$;


the record_manager db table in postgres is getting two copies of a record for some reason.
the easiest thing to do is set the file_id and hash to unique in the database, but is there a way to manage it via n8n which is sending the two requests.

embeddings 1536: rjmalagon/gte-qwen2-1.5b-instruct-embed-f16:latest

n8n-nodes-docx-converter to convert word docx to text