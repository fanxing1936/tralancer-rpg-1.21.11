schedule function rpg:town/demon/sec 20t
execute as @a[scores={rpg_dm_do=1..}] at @s run function rpg:town/demon/do
execute as @a[scores={rpg_ident=4},tag=!rpg.dm] run function rpg:town/demon/born
execute as @a[tag=rpg.dm] at @s run function rpg:town/demon/each
function rpg:town/demon/job_tick
