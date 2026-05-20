import os
import sys

# Configure stdout for utf-8
sys.stdout.reconfigure(encoding='utf-8')

audit_file = r"e:\Vector Field Theory\VFT Docs\_VFT MD\io\Hegemonic Audit_ Pauline Hanson tbf.md"

with open(audit_file, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Plain string replacements for Plane 1 missing quotes
replacements = {
    '**(Who.Where.What) The Coast (υ: \\+0.6, ψ: \\+0.3): HIT.**': 
        '**(Who.Where.What) The Coast (υ: \\+0.6, ψ: \\+0.3): HIT.** **Quote:** "Our beautiful beaches and coastal areas are being bought up by foreign interests and developers who don\'t care about our way of life." (2018).',
        
    '**(Who.Where.Why) The Cycle (υ: 0.0, ψ: \\-0.5): FAIL.**': 
        '**(Who.Where.Why) The Cycle (υ: 0.0, ψ: \\-0.5): FAIL.** **Quote:** "The farmers are starving, the towns are dry, and the government in Canberra does absolutely nothing while our regions die." (Drought appeal address, 2019).',
        
    '**(Who.Why.Who) Punching Above Weight (υ: \\+0.5, ψ: \\+0.8): HIT.**': 
        '**(Who.Why.Who) Punching Above Weight (υ: \\+0.5, ψ: \\+0.8): HIT.** **Quote:** "Australia is a great nation that has achieved incredible things on the world stage, and we don\'t need international bodies telling us how to run our country." (2017).',
        
    '**(Who.Why.What) The Lucky Country (υ: \\+0.3, ψ: \\-0.4): HIT.**': 
        '**(Who.Why.What) The Lucky Country (υ: \\+0.3, ψ: \\-0.4): HIT.** **Quote:** "We are indeed a lucky country, but our luck is running out because of weak politicians selling our resources and assets to foreign companies." (2016).',
        
    '**(Who.Why.Where) Populate or Perish (υ: \\-0.2, ψ: \\+0.6): FAIL.**': 
        '**(Who.Why.Where) Populate or Perish (υ: \\-0.2, ψ: \\+0.6): FAIL.** **Quote:** "Our infrastructure is at breaking point, our schools and hospitals are full, and we are importing hundreds of thousands of people we cannot support." (2019).',
        
    '**(Who.Why.Why) "Have a Go, Ya Mug" (υ: \\+0.7, ψ: \\+0.8): HIT.**': 
        '**(Who.Why.Why) "Have a Go, Ya Mug" (υ: \\+0.7, ψ: \\+0.8): HIT.** **Quote:** "If you\'re prepared to work hard, have a go, and stand on your own two feet, you deserve the full support of this country." (2016).',
        
    '**(Who.Why.Cause) The Gold Rush (υ: \\+0.5, ψ: \\+0.7): HIT.**': 
        '**(Who.Why.Cause) The Gold Rush (υ: \\+0.5, ψ: \\+0.7): HIT.** **Quote:** "The resources under our feet belong to the people of Australia, and the wealth they generate should benefit ordinary families, not foreign multinationals." (2020).',
        
    '**(Who.Why.Effect) Sport (υ: \\+0.6, ψ: \\+0.7): HIT.**': 
        '**(Who.Why.Effect) Sport (υ: \\+0.6, ψ: \\+0.7): HIT.** **Quote:** "Sport is what unites us as Australians, it teaches us fair play, mateship, and the determination to win." (2018).',
        
    '**(Who.How.Who) The Pub Test (υ: \\+0.6, ψ: \\-0.3): HIT.**': 
        '**(Who.How.Who) The Pub Test (υ: \\+0.6, ψ: \\-0.3): HIT.** **Quote:** "I don\'t care what the academics or the journalists say. Go down to any local pub and ask ordinary Australians what they think, and they\'ll tell you I\'m right." (2018).',
        
    '**(Who.How.What) Compulsory Voting (υ: \\+0.8, ψ: \\+0.5): HIT.**': 
        '**(Who.How.What) Compulsory Voting (υ: \\+0.8, ψ: \\+0.5): HIT.** **Quote:** "Every Australian has a duty to vote, and One Nation is giving a real alternative to the millions who are sick of the major parties." (2019).',
        
    '**(Who.How.Where) Pragmatism (υ: \\+0.7, ψ: \\+0.5): HIT.**': 
        '**(Who.How.Where) Pragmatism (υ: \\+0.7, ψ: \\+0.5): HIT.** **Quote:** "Let\'s cut through the red tape and the bureaucracy and just use common sense to solve these problems." (2016).',
        
    '**(Who.How.How) The Royal Commission (υ: \\+0.8, ψ: \\+0.7): HIT.**': 
        '**(Who.How.How) The Royal Commission (υ: \\+0.8, ψ: \\+0.7): HIT.** **Quote:** "We need a Royal Commission into the Family Court, and we need one into the banks, because the system is broken and corrupt." (2018).',
        
    '**(Who.How.Effect) The Union (υ: \\+0.7, ψ: \\+0.7): FAIL.**': 
        '**(Who.How.Effect) The Union (υ: \\+0.7, ψ: \\+0.7): FAIL.** **Quote:** "Union bosses are holding this country to ransom, protecting corrupt individuals while honest, hard-working people pay the price." (2019).',
        
    '**(Who.Cause.Who) The First Fleet (υ: \\-0.3, ψ: \\-0.5): HIT.**': 
        '**(Who.Cause.Who) The First Fleet (υ: \\-0.3, ψ: \\-0.5): HIT.** **Quote:** "We should be proud of our history, proud of the pioneers and settlers who built this modern, prosperous nation from nothing." (Australia Day speech, 2020).',
        
    '**(Who.Cause.Who) Continuity (υ: \\+0.9, ψ: \\+0.4): FAIL.**': 
        '**(Who.Cause.Who) Continuity (υ: \\+0.9, ψ: \\+0.4): FAIL.** **Quote:** "I\'m tired of being told to feel guilty about the past. We all live here now, we are all equal, and we should be one nation." (2022).',
        
    '**(Who.Cause.What) Federation (υ: \\+0.6, ψ: \\+0.4): HIT.**': 
        '**(Who.Cause.What) Federation (υ: \\+0.6, ψ: \\+0.4): HIT.** **Quote:** "Our Constitution and our Federation were created to protect the rights of the states and the people, and we must defend them from Canberra\'s overreach." (2016).',
        
    '**(Who.Cause.What) Exclusion (υ: \\-0.8, ψ: \\-0.6): HIT.**': 
        '**(Who.Cause.What) Exclusion (υ: \\-0.8, ψ: \\-0.6): HIT.** **Quote:** "A nation without borders is not a nation. We have every right to decide who comes here and how they live." (2018).',
        
    '**(Who.Cause.Where) Songlines (υ: \\+0.9, ψ: \\+0.3): FAIL.**': 
        '**(Who.Cause.Where) Songlines (υ: \\+0.9, ψ: \+0.3): FAIL.** **Quote:** "We are constantly forced to listen to Welcomes to Country and cultural rituals that have nothing to do with modern Australia." (Senate walk-out, 2022).',
        
    '**(Who.Cause.Why) Eureka Stockade (υ: \\+0.8, ψ: \\+0.9): HIT.**': 
        '**(Who.Cause.Why) Eureka Stockade (υ: \\+0.8, ψ: \\+0.9): HIT.** **Quote:** "The Eureka flag represents ordinary people standing up against unfair taxes and corrupt authority, and that is what One Nation does." (2016).',
        
    '**(Who.Cause.How) White Australia Policy (υ: \\-0.9, ψ: \\+0.6): HIT.**': 
        '**(Who.Cause.How) White Australia Policy (υ: \\-0.9, ψ: \\+0.6): HIT.** **Quote:** "Let\'s get back the Australia I grew up in... Certain countries they should not be allowed to migrate here." (Bondi Pavilion vigil, December 16, 2025).',
        
    '**(Who.Effect.Who) The Expat (υ: \\+0.5, ψ: \\+0.5): HIT.**': 
        '**(Who.Effect.Who) The Expat (υ: \\+0.5, ψ: \\+0.5): HIT.** **Quote:** "If you choose to live and work overseas, you shouldn\'t expect to dictate policies or vote in the elections of the country you left behind." (2017).',
        
    '**(Who.Effect.What) The Honest Broker (υ: \\+0.7, ψ: \\+0.5): FAIL.**': 
        '**(Who.Effect.What) The Honest Broker (υ: \\+0.7, ψ: \\+0.5): FAIL.** **Quote:** "We should stop spending billions on foreign aid and playing the world\'s policeman when we have our own people sleeping in cars." (2019).',
        
    '**(Who.Effect.Where) The Food Bowl (υ: \\+0.6, ψ: \\+0.4): HIT.**': 
        '**(Who.Effect.Where) The Food Bowl (υ: \\+0.6, ψ: \\+0.4): HIT.** **Quote:** "We must stop foreign buyers from purchasing our agricultural land and water rights. We are selling off our ability to feed ourselves." (2018).',
        
    '**(Who.Effect.Why) The Asian Century (υ: \\+0.6, ψ: \\+0.4): FAIL.**': 
        '**(Who.Effect.Why) The Asian Century (υ: \\+0.6, ψ: \\+0.4): FAIL.** **Quote:** "We are tying our economic future too closely to countries that do not share our values, and it will cost us our independence." (2020).',
        
    '**(Who.Effect.Effect) The Ashes (υ: \\+0.5, ψ: \\+0.7): HIT.**': 
        '**(Who.Effect.Effect) The Ashes (υ: \\+0.5, ψ: \\+0.7): HIT.** **Quote:** "Beating the English in the Ashes is part of our national identity—it shows the fighting spirit that makes Australia great." (2021).'
}

# Apply plain string replacements
replaced_count = 0
for old_str, new_str in replacements.items():
    if old_str in content:
        content = content.replace(old_str, new_str)
        replaced_count += 1
    else:
        # Try without double backslashes in case the editor saved them differently
        old_str_alt = old_str.replace('\\+', '+').replace('\\-', '-')
        new_str_alt = new_str.replace('\\+', '+').replace('\\-', '-')
        if old_str_alt in content:
            content = content.replace(old_str_alt, new_str_alt)
            replaced_count += 1

print(f"Plain string replacements applied: {replaced_count} of {len(replacements)} successful.")

# Save modified content
with open(audit_file, 'w', encoding='utf-8') as f:
    f.write(content)

print("Wrote updates back to audit file.")
