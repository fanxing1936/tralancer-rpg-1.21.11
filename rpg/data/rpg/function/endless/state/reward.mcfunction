scoreboard players add @s rpg_end_time 1
scoreboard players enable @a[tag=rpg.end.member.current] rpg_end_pick
execute as @a[tag=rpg.end.member.current,scores={rpg_end_claim=0,rpg_end_pick=1..3}] run function rpg:endless/reward/claim
execute if score @s rpg_end_time matches 400.. run function rpg:endless/reward/timeout
execute unless entity @a[tag=rpg.end.member.current,scores={rpg_end_claim=0},limit=1] run function rpg:endless/reward/close
