# 开一层（at 中心）
scoreboard players set #c2 rpg_pl 1
scoreboard players set #r2 rpg_pl 0
scoreboard players operation #n rpg_pl = #l2 rpg_pl
scoreboard players add #n rpg_pl 5
execute store result storage rpg:paradise c.n int 1 run scoreboard players get #n rpg_pl
setblock ~ ~1 ~ minecraft:air
setblock ~ ~1 ~ minecraft:trial_spawner[ominous=false]{normal_config:{spawn_potentials:[{data:{entity:{id:"minecraft:spider",drop_chances:{mainhand:0f,offhand:0f,head:0f,chest:0f},Health:36f,attributes:[{id:"minecraft:max_health",base:36d},{id:"minecraft:attack_damage",base:5d}]}},weight:3},{data:{entity:{id:"minecraft:cave_spider",drop_chances:{mainhand:0f,offhand:0f,head:0f,chest:0f},Health:36f,attributes:[{id:"minecraft:max_health",base:36d},{id:"minecraft:attack_damage",base:5d}]}},weight:2},{data:{entity:{id:"minecraft:creeper",drop_chances:{mainhand:0f,offhand:0f,head:0f,chest:0f},Health:36f,attributes:[{id:"minecraft:max_health",base:36d},{id:"minecraft:attack_damage",base:5d}]}},weight:2},{data:{entity:{id:"minecraft:zombie",equipment:{mainhand:{id:"minecraft:iron_sword",count:1},head:{id:"minecraft:iron_helmet",count:1}},drop_chances:{mainhand:0f,offhand:0f,head:0f,chest:0f},Health:36f,attributes:[{id:"minecraft:max_health",base:36d},{id:"minecraft:attack_damage",base:5d}]}},weight:1}],loot_tables_to_eject:[{data:"rpg:paradise/court_2",weight:1}],simultaneous_mobs:4f,simultaneous_mobs_added_per_player:1f,ticks_between_spawn:6,total_mobs:15f,total_mobs_added_per_player:2f,spawn_range:4},spawn_data:{entity:{id:"minecraft:spider",drop_chances:{mainhand:0f,offhand:0f,head:0f,chest:0f},Health:36f,attributes:[{id:"minecraft:max_health",base:36d},{id:"minecraft:attack_damage",base:5d}]}},required_player_range:16,target_cooldown_length:36000}
effect give @a[distance=..24] minecraft:instant_health 1 1 true
execute as @a[distance=..24,scores={rpg_force=1}] run scoreboard players add @s rpg_mana 20
execute as @a[distance=..24,scores={rpg_force=2..3}] run scoreboard players add @s rpg_mana 20
particle minecraft:trial_spawner_detection ~ ~2 ~ 1 1 1 0.2 200
function rpg:pl/court/2/title with storage rpg:paradise c
summon minecraft:ominous_item_spawner ~2 ~6 ~2 {item:{id:"minecraft:wind_charge",count:1},spawn_item_after_ticks:100L}
summon minecraft:ominous_item_spawner ~-2 ~6 ~2 {item:{id:"minecraft:wind_charge",count:1},spawn_item_after_ticks:120L}
summon minecraft:ominous_item_spawner ~1 ~5 ~-3 {item:{id:"minecraft:lingering_potion",count:1,components:{"minecraft:potion_contents":{custom_color:6268978,custom_effects:[{id:"minecraft:poison",duration:200,amplifier:1}]}}},spawn_item_after_ticks:50L}
summon minecraft:ominous_item_spawner ~-2 ~6 ~-2 {item:{id:"minecraft:lingering_potion",count:1,components:{"minecraft:potion_contents":{custom_color:4673362,custom_effects:[{id:"minecraft:wither",duration:120,amplifier:2}]}}},spawn_item_after_ticks:80L}
execute if score #l2 rpg_pl matches 5 positioned ~ ~ ~4 run function rpg:pl/court/guard_2
execute if score #l2 rpg_pl matches 1 as @a[distance=..24] at @s run playsound rpg:bgm.prologue_waves record @s ~ ~ ~ 0.6 1
