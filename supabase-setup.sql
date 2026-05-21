-- ═══════════════════════════════════════
-- STEP 1: CREATE ALL TABLES FIRST
-- ═══════════════════════════════════════

create table if not exists public.materials (
  id uuid primary key default gen_random_uuid(),
  created_at timestamptz default now(),
  title text not null,
  description text,
  module text not null,
  type text default 'link',
  url text,
  file_path text,
  sort_order int default 0,
  is_published boolean default true,
  uploaded_by text
);

create table if not exists public.services (
  id uuid primary key default gen_random_uuid(),
  created_at timestamptz default now(),
  title text not null,
  description text,
  icon text default '🔬',
  price text,
  page text default 'diagnostic',
  link text,
  sort_order int default 0,
  is_published boolean default true
);

create table if not exists public.admins (
  id uuid primary key default gen_random_uuid(),
  email text unique not null,
  name text,
  created_at timestamptz default now()
);

-- ═══════════════════════════════════════
-- STEP 2: ENABLE SECURITY
-- ═══════════════════════════════════════

alter table public.materials enable row level security;
alter table public.services enable row level security;
alter table public.admins enable row level security;

drop policy if exists "Public can read published materials" on public.materials;
drop policy if exists "Authenticated full access materials" on public.materials;
drop policy if exists "Public can read published services" on public.services;
drop policy if exists "Authenticated full access services" on public.services;
drop policy if exists "Admins table read" on public.admins;

create policy "Public can read published materials"
  on public.materials for select using (is_published = true);

create policy "Authenticated full access materials"
  on public.materials for all to authenticated
  using (true) with check (true);

create policy "Public can read published services"
  on public.services for select using (is_published = true);

create policy "Authenticated full access services"
  on public.services for all to authenticated
  using (true) with check (true);

create policy "Admins table read"
  on public.admins for select to authenticated using (true);

create policy "Admins table write"
  on public.admins for all to authenticated
  using (true) with check (true);

-- ═══════════════════════════════════════
-- STEP 3: STORAGE BUCKET
-- ═══════════════════════════════════════

insert into storage.buckets (id, name, public)
  values ('materials', 'materials', true)
  on conflict (id) do nothing;

drop policy if exists "Auth users can upload materials" on storage.objects;
drop policy if exists "Public can read materials" on storage.objects;
drop policy if exists "Auth users can delete materials" on storage.objects;

create policy "Auth users can upload materials"
  on storage.objects for insert to authenticated
  with check (bucket_id = 'materials');

create policy "Public can read materials"
  on storage.objects for select
  using (bucket_id = 'materials');

create policy "Auth users can delete materials"
  on storage.objects for delete to authenticated
  using (bucket_id = 'materials');

-- ═══════════════════════════════════════
-- STEP 4: ADD YOUR ADMIN USER
-- ═══════════════════════════════════════

insert into public.admins (email, name)
values ('rmetim@icloud.com', 'Site Admin')
on conflict (email) do nothing;
