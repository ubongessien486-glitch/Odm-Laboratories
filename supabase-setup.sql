-- ═══════════════════════════════════════
-- OXYGEN GROUP — ADMIN PANEL DATABASE SETUP
-- Run this entire block in Supabase SQL Editor
-- ═══════════════════════════════════════

-- 1. Materials table (Learning Hub uploads)
create table if not exists public.materials (
  id uuid primary key default gen_random_uuid(),
  created_at timestamptz default now(),
  title text not null,
  description text,
  module text not null,
  type text default 'link', -- 'link' | 'file' | 'video'
  url text,
  file_path text,
  sort_order int default 0,
  is_published boolean default true,
  uploaded_by text
);

-- 2. Services table (editable service cards)
create table if not exists public.services (
  id uuid primary key default gen_random_uuid(),
  created_at timestamptz default now(),
  title text not null,
  description text,
  icon text default '🔬',
  price text,
  page text default 'diagnostic', -- which page it appears on
  link text,
  sort_order int default 0,
  is_published boolean default true
);

-- 3. Admins table (who can access admin panel)
create table if not exists public.admins (
  id uuid primary key default gen_random_uuid(),
  email text unique not null,
  name text,
  created_at timestamptz default now()
);

-- 4. Enable Row Level Security (RLS) but allow anon reads for published content
alter table public.materials enable row level security;
alter table public.services enable row level security;
alter table public.admins enable row level security;

-- Allow anyone logged in to read published materials
create policy "Public can read published materials"
  on public.materials for select
  using (is_published = true);

-- Allow anyone logged in to read published services
create policy "Public can read published services"
  on public.services for select
  using (is_published = true);

-- Allow authenticated users to do everything (admin writes)
create policy "Authenticated full access materials"
  on public.materials for all
  to authenticated
  using (true) with check (true);

create policy "Authenticated full access services"
  on public.services for all
  to authenticated
  using (true) with check (true);

create policy "Admins table read"
  on public.admins for select
  to authenticated
  using (true);

-- 5. Create storage bucket for file uploads
insert into storage.buckets (id, name, public)
  values ('materials', 'materials', true)
  on conflict (id) do nothing;

-- Allow authenticated users to upload to materials bucket
create policy "Auth users can upload materials"
  on storage.objects for insert
  to authenticated
  with check (bucket_id = 'materials');

create policy "Public can read materials"
  on storage.objects for select
  using (bucket_id = 'materials');

create policy "Auth users can delete materials"
  on storage.objects for delete
  to authenticated
  using (bucket_id = 'materials');

-- ═══════════════════════════════════════
-- DONE. Now add your first admin email:
-- ═══════════════════════════════════════
-- INSERT INTO public.admins (email, name) 
-- VALUES ('your-admin-email@example.com', 'Admin Name');
