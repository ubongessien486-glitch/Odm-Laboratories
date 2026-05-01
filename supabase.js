import { createClient } from 'https://cdn.jsdelivr.net/npm/@supabase/supabase-js/+esm'

const supabaseUrl = 'https://jzlkovnrymlwkuvbewkc.supabase.co'
const supabaseKey = 'sb_publishable_lORAx-U_P3YiIjiR9ekd6w_Bd2hnP4S'

export const supabase = createClient(supabaseUrl, supabaseKey)

// Make it available globally so inline scripts can use it
window.supabaseClient = supabase;
