execute if score @s rpg_dm_lord matches 1 as @a[tag=rpg.rite.chooser,distance=..14,limit=1] run function rpg:inquest/give/relic1
execute if score @s rpg_dm_lord matches 2 as @a[tag=rpg.rite.chooser,distance=..14,limit=1] run function rpg:inquest/give/relic2
execute if score @s rpg_dm_lord matches 3 as @a[tag=rpg.rite.chooser,distance=..14,limit=1] run function rpg:inquest/give/relic3
execute if score @s rpg_dm_lord matches 4 as @a[tag=rpg.rite.chooser,distance=..14,limit=1] run function rpg:inquest/give/relic4
execute if score @s rpg_dm_lord matches 5 as @a[tag=rpg.rite.chooser,distance=..14,limit=1] run function rpg:inquest/give/relic5
execute if score @s rpg_dm_lord matches 6 as @a[tag=rpg.rite.chooser,distance=..14,limit=1] run function rpg:inquest/give/relic6
execute if score @s rpg_dm_lord matches 7 as @a[tag=rpg.rite.chooser,distance=..14,limit=1] run function rpg:inquest/give/relic7
tag @a[tag=rpg.rite.chooser,distance=..14] add rpg.seal.carrier
scoreboard players add @a[tag=rpg.rite.chooser,distance=..14] rpg_ex_xp 18
scoreboard players add @a[tag=rpg.rite.chooser,distance=..14] rpg_taint 5

execute on passengers run kill @s
particle sculk_soul ~ ~1 ~ 1.2 1.2 1.2 0.12 80 force
kill @s
