# 称量［TEKEL］——"你被称在天平里，显出你的亏欠"（但以理书 5:27）
# 判决直接读 damage_action：那是 rpg:command/index 每刻已经抓好的血量，零额外开销。
xp add @s -1 levels
tag @s add rpg.jachin.cast
execute if entity @s[tag=rpg.twin] run tag @s add rpg.jachin.temple

particle dust_color_transition{from_color:[0.478,0.086,0.584],to_color:[0.949,0.851,0.404],scale:1} ~ ~1 ~ 0.3 0.4 0.3 0.02 12
playsound minecraft:block.enchantment_table.use player @a[distance=..16] ~ ~ ~ 1 0.7
playsound minecraft:entity.evoker.prepare_summon player @a[distance=..16] ~ ~ ~ 0.6 1.4

execute unless entity @s[tag=rpg.twin] as @e[distance=0.1..6,type=!player,type=!minecraft:item,type=!minecraft:experience_orb] at @s run function rpg:item/extra/jachin_weigh
execute if entity @s[tag=rpg.twin] as @e[distance=0.1..9,type=!player,type=!minecraft:item,type=!minecraft:experience_orb] at @s run function rpg:item/extra/jachin_weigh
execute if entity @s[tag=rpg.twin] run effect give @s minecraft:absorption 8 1 true
execute if entity @s[tag=rpg.twin] run playsound minecraft:block.respawn_anchor.charge player @a[distance=..16]

tag @s remove rpg.jachin.cast
tag @s remove rpg.jachin.temple
