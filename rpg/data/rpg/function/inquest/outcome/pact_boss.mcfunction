execute if score @s rpg_dm_lord matches 1 as @a[tag=rpg.rite.chooser,distance=..14,limit=1] run function rpg:inquest/give/pact1
execute if score @s rpg_dm_lord matches 1 as @a[tag=rpg.rite.chooser,distance=..14,limit=1] run function rpg:inquest/give/pact_weapon1
execute if score @s rpg_dm_lord matches 2 as @a[tag=rpg.rite.chooser,distance=..14,limit=1] run function rpg:inquest/give/pact2
execute if score @s rpg_dm_lord matches 2 as @a[tag=rpg.rite.chooser,distance=..14,limit=1] run function rpg:inquest/give/pact_weapon2
execute if score @s rpg_dm_lord matches 3 as @a[tag=rpg.rite.chooser,distance=..14,limit=1] run function rpg:inquest/give/pact3
execute if score @s rpg_dm_lord matches 3 as @a[tag=rpg.rite.chooser,distance=..14,limit=1] run function rpg:inquest/give/pact_weapon3
execute if score @s rpg_dm_lord matches 4 as @a[tag=rpg.rite.chooser,distance=..14,limit=1] run function rpg:inquest/give/pact4
execute if score @s rpg_dm_lord matches 4 as @a[tag=rpg.rite.chooser,distance=..14,limit=1] run function rpg:inquest/give/pact_weapon4
execute if score @s rpg_dm_lord matches 5 as @a[tag=rpg.rite.chooser,distance=..14,limit=1] run function rpg:inquest/give/pact5
execute if score @s rpg_dm_lord matches 5 as @a[tag=rpg.rite.chooser,distance=..14,limit=1] run function rpg:inquest/give/pact_weapon5
execute if score @s rpg_dm_lord matches 6 as @a[tag=rpg.rite.chooser,distance=..14,limit=1] run function rpg:inquest/give/pact6
execute if score @s rpg_dm_lord matches 6 as @a[tag=rpg.rite.chooser,distance=..14,limit=1] run function rpg:inquest/give/pact_weapon6
execute if score @s rpg_dm_lord matches 7 as @a[tag=rpg.rite.chooser,distance=..14,limit=1] run function rpg:inquest/give/pact7
execute if score @s rpg_dm_lord matches 7 as @a[tag=rpg.rite.chooser,distance=..14,limit=1] run function rpg:inquest/give/pact_weapon7
scoreboard players add @a[tag=rpg.rite.chooser,distance=..14] rpg_ex_xp 15
scoreboard players add @a[tag=rpg.rite.chooser,distance=..14] rpg_taint 25

execute on passengers run kill @s
particle sculk_soul ~ ~1 ~ 1.2 1.2 1.2 0.12 80 force
kill @s
