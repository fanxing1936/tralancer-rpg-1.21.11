# Only newly seen mobs are mutated; normal item entities are never scanned or removed.
execute as @e[type=#rpg:drop_policy_mobs,tag=!rpg.drop_policy.v1] run function rpg:drop_policy/prepare
