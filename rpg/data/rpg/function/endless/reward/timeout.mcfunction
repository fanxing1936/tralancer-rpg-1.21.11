scoreboard players set @a[tag=rpg.end.member.current,scores={rpg_end_claim=0}] rpg_end_pick 3
execute as @a[tag=rpg.end.member.current,scores={rpg_end_claim=0}] run function rpg:endless/reward/claim
