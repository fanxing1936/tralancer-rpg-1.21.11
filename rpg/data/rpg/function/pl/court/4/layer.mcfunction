# 开一层（at 中心）
scoreboard players set #c4 rpg_pl 1
scoreboard players set #r4 rpg_pl 0
scoreboard players operation #n rpg_pl = #l4 rpg_pl
scoreboard players add #n rpg_pl 15
execute store result storage rpg:paradise c.n int 1 run scoreboard players get #n rpg_pl
setblock ~ ~2 ~ minecraft:air
setblock ~ ~2 ~ minecraft:trial_spawner[ominous=true]{ominous_config:{spawn_potentials:[{data:{entity:{id:"minecraft:wither_skeleton",equipment:{mainhand:{id:"minecraft:stone_sword",count:1}},drop_chances:{mainhand:0f,offhand:0f,head:0f,chest:0f},Health:54f,attributes:[{id:"minecraft:max_health",base:54d},{id:"minecraft:attack_damage",base:9d}]}},weight:3},{data:{entity:{id:"minecraft:stray",equipment:{mainhand:{id:"minecraft:bow",count:1},head:{id:"minecraft:iron_helmet",count:1}},drop_chances:{mainhand:0f,offhand:0f,head:0f,chest:0f},Health:54f,attributes:[{id:"minecraft:max_health",base:54d},{id:"minecraft:attack_damage",base:9d}]}},weight:2},{data:{entity:{id:"minecraft:enderman",drop_chances:{mainhand:0f,offhand:0f,head:0f,chest:0f},Health:54f,attributes:[{id:"minecraft:max_health",base:54d},{id:"minecraft:attack_damage",base:9d}]}},weight:1},{data:{entity:{id:"minecraft:husk",equipment:{mainhand:{id:"minecraft:iron_axe",count:1},chest:{id:"minecraft:iron_chestplate",count:1}},drop_chances:{mainhand:0f,offhand:0f,head:0f,chest:0f},Health:54f,attributes:[{id:"minecraft:max_health",base:54d},{id:"minecraft:attack_damage",base:9d}]}},weight:2}],loot_tables_to_eject:[{data:"rpg:paradise/court_4",weight:1}],simultaneous_mobs:5f,simultaneous_mobs_added_per_player:3f,ticks_between_spawn:6,total_mobs:30f,total_mobs_added_per_player:4f,spawn_range:7},spawn_data:{entity:{id:"minecraft:wither_skeleton",equipment:{mainhand:{id:"minecraft:stone_sword",count:1}},drop_chances:{mainhand:0f,offhand:0f,head:0f,chest:0f},Health:54f,attributes:[{id:"minecraft:max_health",base:54d},{id:"minecraft:attack_damage",base:9d}]}},required_player_range:16,target_cooldown_length:36000}
effect give @a[distance=..24] minecraft:instant_health 1 1 true
execute as @a[distance=..24,scores={rpg_force=1}] run scoreboard players add @s rpg_mana 20
execute as @a[distance=..24,scores={rpg_force=2..3}] run scoreboard players add @s rpg_mana 20
particle minecraft:trial_spawner_detection_ominous ~ ~2 ~ 1 1 1 0.2 200
function rpg:pl/court/4/title with storage rpg:paradise c
summon minecraft:ominous_item_spawner ~3 ~6 ~3 {item:{id:"minecraft:wind_charge",count:1},spawn_item_after_ticks:100L}
summon minecraft:ominous_item_spawner ~-3 ~6 ~4 {item:{id:"minecraft:wind_charge",count:1},spawn_item_after_ticks:120L}
summon minecraft:ominous_item_spawner ~1 ~5 ~-5 {item:{id:"minecraft:lingering_potion",count:1,components:{"minecraft:potion_contents":{custom_color:6268978,custom_effects:[{id:"minecraft:poison",duration:200,amplifier:1}]}}},spawn_item_after_ticks:50L}
summon minecraft:ominous_item_spawner ~-4 ~6 ~-3 {item:{id:"minecraft:lingering_potion",count:1,components:{"minecraft:potion_contents":{custom_color:4673362,custom_effects:[{id:"minecraft:wither",duration:120,amplifier:2}]}}},spawn_item_after_ticks:80L}
summon minecraft:ominous_item_spawner ~6 ~6 ~-5 {item:{id:"minecraft:lingering_potion",count:1,components:{"minecraft:potion_contents":{custom_color:7733497,custom_effects:[{id:"minecraft:darkness",duration:600,amplifier:1},{id:"minecraft:nausea",duration:600,amplifier:1},{id:"minecraft:slowness",duration:600,amplifier:2}]}}},spawn_item_after_ticks:150L}
summon minecraft:ominous_item_spawner ~-5 ~5 ~5 {item:{id:"minecraft:lingering_potion",count:1,components:{"minecraft:potion_contents":{potion:"minecraft:strong_harming"}}},spawn_item_after_ticks:110L}
execute if score #l4 rpg_pl matches 5 positioned ~ ~ ~5 run function rpg:pl/court/guard_4
