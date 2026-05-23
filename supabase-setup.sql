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

-- New tables for CRM Leads, Patient Intakes, and Referral Sources
create table if not exists public.crm_leads (
  id uuid primary key default gen_random_uuid(),
  created_at timestamptz default now(),
  name text not null,
  email text,
  phone text,
  subject text,
  message text,
  status text default 'New'
);

create table if not exists public.patient_intake (
  id uuid primary key default gen_random_uuid(),
  created_at timestamptz default now(),
  patient_name text not null,
  phone text not null,
  email text,
  location text,
  urgency text,
  care_needs text,
  status text default '1. New Inquiry'
);

create table if not exists public.referral_sources (
  id uuid primary key default gen_random_uuid(),
  created_at timestamptz default now(),
  name text not null,
  facility text,
  role text,
  phone text,
  email text,
  pain_points text,
  fast_response_requested boolean default false,
  pipeline_stage text default '1. New Contact'
);

-- ═══════════════════════════════════════
-- STEP 2: ENABLE SECURITY (RLS)
-- ═══════════════════════════════════════

alter table public.materials enable row level security;
alter table public.services enable row level security;
alter table public.admins enable row level security;
alter table public.crm_leads enable row level security;
alter table public.patient_intake enable row level security;
alter table public.referral_sources enable row level security;

-- Drop old policies if they exist to prevent conflicts
drop policy if exists "Public can read published materials" on public.materials;
drop policy if exists "Authenticated full access materials" on public.materials;
drop policy if exists "Admins write access materials" on public.materials;
drop policy if exists "Public read materials" on public.materials;

drop policy if exists "Public can read published services" on public.services;
drop policy if exists "Authenticated full access services" on public.services;
drop policy if exists "Admins write access services" on public.services;
drop policy if exists "Public read services" on public.services;

drop policy if exists "Admins table read" on public.admins;
drop policy if exists "Admins table write" on public.admins;
drop policy if exists "Admins table admin write" on public.admins;

drop policy if exists "Public can insert leads" on public.crm_leads;
drop policy if exists "Admins full access leads" on public.crm_leads;

drop policy if exists "Public can insert patient intake" on public.patient_intake;
drop policy if exists "Admins full access patient intake" on public.patient_intake;

drop policy if exists "Public can insert referrals" on public.referral_sources;
drop policy if exists "Admins full access referrals" on public.referral_sources;

-- Create secure, role-based policies
-- 1. Materials
create policy "Public read materials"
  on public.materials for select using (true);

create policy "Admins write access materials"
  on public.materials for all to authenticated
  using (exists (select 1 from public.admins where email = auth.jwt()->>'email'))
  with check (exists (select 1 from public.admins where email = auth.jwt()->>'email'));

-- 2. Services
create policy "Public read services"
  on public.services for select using (true);

create policy "Admins write access services"
  on public.services for all to authenticated
  using (exists (select 1 from public.admins where email = auth.jwt()->>'email'))
  with check (exists (select 1 from public.admins where email = auth.jwt()->>'email'));

-- 3. Admins
create policy "Admins table read"
  on public.admins for select to authenticated using (true);

create policy "Admins table admin write"
  on public.admins for all to authenticated
  using (exists (select 1 from public.admins where email = auth.jwt()->>'email'))
  with check (exists (select 1 from public.admins where email = auth.jwt()->>'email'));

-- 4. CRM Leads (Public can insert, only Admins can read/write)
create policy "Public can insert leads"
  on public.crm_leads for insert with check (true);

create policy "Admins full access leads"
  on public.crm_leads for all to authenticated
  using (exists (select 1 from public.admins where email = auth.jwt()->>'email'))
  with check (exists (select 1 from public.admins where email = auth.jwt()->>'email'));

-- 5. Patient Intake (Public can insert, only Admins can read/write)
create policy "Public can insert patient intake"
  on public.patient_intake for insert with check (true);

create policy "Admins full access patient intake"
  on public.patient_intake for all to authenticated
  using (exists (select 1 from public.admins where email = auth.jwt()->>'email'))
  with check (exists (select 1 from public.admins where email = auth.jwt()->>'email'));

-- 6. Referral Sources (Public can insert, only Admins can read/write)
create policy "Public can insert referrals"
  on public.referral_sources for insert with check (true);

create policy "Admins full access referrals"
  on public.referral_sources for all to authenticated
  using (exists (select 1 from public.admins where email = auth.jwt()->>'email'))
  with check (exists (select 1 from public.admins where email = auth.jwt()->>'email'));

-- ═══════════════════════════════════════
-- STEP 3: STORAGE BUCKET
-- ═══════════════════════════════════════

insert into storage.buckets (id, name, public)
  values ('materials', 'materials', true)
  on conflict (id) do nothing;

drop policy if exists "Auth users can upload materials" on storage.objects;
drop policy if exists "Public can read materials" on storage.objects;
drop policy if exists "Auth users can delete materials" on storage.objects;
drop policy if exists "Admins can upload materials" on storage.objects;
drop policy if exists "Admins can delete materials" on storage.objects;

create policy "Public can read materials"
  on storage.objects for select
  using (bucket_id = 'materials');

create policy "Admins can upload materials"
  on storage.objects for insert to authenticated
  with check (bucket_id = 'materials' and exists (select 1 from public.admins where email = auth.jwt()->>'email'));

create policy "Admins can delete materials"
  on storage.objects for delete to authenticated
  using (bucket_id = 'materials' and exists (select 1 from public.admins where email = auth.jwt()->>'email'));

-- ═══════════════════════════════════════
-- STEP 4: ADD DEFAULT ADMIN USER (EMAIL & PASSWORD)
-- ═══════════════════════════════════════

-- Seed default admin credentials in Supabase Auth & public.admins
do $$
declare
  new_user_id uuid := gen_random_uuid();
begin
  -- Check if user already exists in auth.users
  if not exists (select 1 from auth.users where email = 'admin@oxygendx.com') then
    -- Insert into auth.users (encodes password 'OxygenAdmin2026!' using bcrypt/bf)
    insert into auth.users (
      instance_id,
      id,
      aud,
      role,
      email,
      encrypted_password,
      email_confirmed_at,
      raw_app_meta_data,
      raw_user_meta_data,
      created_at,
      updated_at,
      confirmation_token,
      email_change,
      email_change_token_new,
      recovery_token
    ) values (
      '00000000-0000-0000-0000-000000000000',
      new_user_id,
      'authenticated',
      'authenticated',
      'admin@oxygendx.com',
      crypt('OxygenAdmin2026!', gen_salt('bf')),
      now(),
      '{"provider":"email","providers":["email"]}',
      '{}',
      now(),
      now(),
      '',
      '',
      '',
      ''
    );

    -- Insert into auth.identities to link identity provider
    insert into auth.identities (
      id,
      user_id,
      identity_data,
      provider,
      last_sign_in_at,
      created_at,
      updated_at
    ) values (
      gen_random_uuid(),
      new_user_id,
      format('{"sub":"%s","email":"admin@oxygendx.com"}', new_user_id)::jsonb,
      'email',
      now(),
      now(),
      now()
    );

    -- Insert into public.admins
    insert into public.admins (email, name)
    values ('admin@oxygendx.com', 'System Admin')
    on conflict (email) do nothing;
  end if;

  -- Add second fallback admin record
  insert into public.admins (email, name)
  values ('rmetim@icloud.com', 'Site Admin')
  on conflict (email) do nothing;
end $$;
