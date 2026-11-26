# 重挂路径赐福（as 玩家；rpg:sephira/bonus/apply 末尾，走完、翻面后也调）
attribute @s minecraft:movement_speed modifier remove rpg:pa_32
attribute @s minecraft:fall_damage_multiplier modifier remove rpg:pa_32
attribute @s minecraft:attack_speed modifier remove rpg:pa_30
attribute @s minecraft:oxygen_bonus modifier remove rpg:pa_28
attribute @s minecraft:water_movement_efficiency modifier remove rpg:pa_28
attribute @s minecraft:jump_strength modifier remove rpg:pa_28
attribute @s minecraft:attack_damage modifier remove rpg:pa_27
attribute @s minecraft:armor_toughness modifier remove rpg:pa_27
attribute @s minecraft:movement_efficiency modifier remove rpg:pa_25
attribute @s minecraft:max_health modifier remove rpg:pa_23
attribute @s minecraft:sneaking_speed modifier remove rpg:pa_20
attribute @s minecraft:knockback_resistance modifier remove rpg:pa_19
attribute @s minecraft:attack_speed modifier remove rpg:pa_19
attribute @s minecraft:armor modifier remove rpg:pa_15
attribute @s minecraft:luck modifier remove rpg:pa_14
attribute @s minecraft:max_health modifier remove rpg:pa_14
attribute @s minecraft:armor modifier remove rpg:pa_29n
attribute @s minecraft:movement_speed modifier remove rpg:pa_18s
attribute @s minecraft:armor modifier remove rpg:pa_17o
attribute @s minecraft:attack_damage modifier remove rpg:pa_11x
scoreboard players set @s rpg_pa_xl -1
execute if score @s rpg_ps_32 matches 2 run attribute @s minecraft:movement_speed modifier add rpg:pa_32 0.03 add_multiplied_base
execute if score @s rpg_ps_32 matches 3 run attribute @s minecraft:fall_damage_multiplier modifier add rpg:pa_32 -0.3 add_multiplied_base
execute if score @s rpg_ps_30 matches 3 run attribute @s minecraft:attack_speed modifier add rpg:pa_30 0.03 add_multiplied_base
execute if score @s rpg_ps_28 matches 2 run attribute @s minecraft:oxygen_bonus modifier add rpg:pa_28 1 add_value
execute if score @s rpg_ps_28 matches 2 run attribute @s minecraft:water_movement_efficiency modifier add rpg:pa_28 0.2 add_value
execute if score @s rpg_ps_28 matches 3 run attribute @s minecraft:jump_strength modifier add rpg:pa_28 0.1 add_multiplied_base
execute if score @s rpg_ps_27 matches 2 run attribute @s minecraft:attack_damage modifier add rpg:pa_27 0.03 add_multiplied_base
execute if score @s rpg_ps_27 matches 3 run attribute @s minecraft:armor_toughness modifier add rpg:pa_27 1 add_value
execute if score @s rpg_ps_25 matches 3 run attribute @s minecraft:movement_efficiency modifier add rpg:pa_25 0.3 add_value
execute if score @s rpg_ps_23 matches 3 run attribute @s minecraft:max_health modifier add rpg:pa_23 2 add_value
execute if score @s rpg_ps_20 matches 2 run attribute @s minecraft:sneaking_speed modifier add rpg:pa_20 0.09 add_value
execute if score @s rpg_ps_19 matches 2 run attribute @s minecraft:knockback_resistance modifier add rpg:pa_19 0.15 add_value
execute if score @s rpg_ps_19 matches 3 run attribute @s minecraft:attack_speed modifier add rpg:pa_19 0.04 add_multiplied_base
execute if score @s rpg_ps_15 matches 3 run attribute @s minecraft:armor modifier add rpg:pa_15 2 add_value
execute if score @s rpg_ps_14 matches 2 run attribute @s minecraft:luck modifier add rpg:pa_14 1 add_value
execute if score @s rpg_ps_14 matches 3 run attribute @s minecraft:max_health modifier add rpg:pa_14 2 add_value
execute if score @s rpg_ps_20 matches 3 run scoreboard players add @s rpg_mana_max 10
execute if score @s rpg_ps_13 matches 3 run scoreboard players add @s rpg_mana_max 20
tag @s remove rpg.pa.any
execute if score @s rpg_ps_32 matches 2..3 run tag @s add rpg.pa.any
execute if score @s rpg_ps_31 matches 2..3 run tag @s add rpg.pa.any
execute if score @s rpg_ps_30 matches 2..3 run tag @s add rpg.pa.any
execute if score @s rpg_ps_29 matches 2..3 run tag @s add rpg.pa.any
execute if score @s rpg_ps_28 matches 2..3 run tag @s add rpg.pa.any
execute if score @s rpg_ps_27 matches 2..3 run tag @s add rpg.pa.any
execute if score @s rpg_ps_26 matches 2..3 run tag @s add rpg.pa.any
execute if score @s rpg_ps_25 matches 2..3 run tag @s add rpg.pa.any
execute if score @s rpg_ps_24 matches 2..3 run tag @s add rpg.pa.any
execute if score @s rpg_ps_23 matches 2..3 run tag @s add rpg.pa.any
execute if score @s rpg_ps_22 matches 2..3 run tag @s add rpg.pa.any
execute if score @s rpg_ps_21 matches 2..3 run tag @s add rpg.pa.any
execute if score @s rpg_ps_20 matches 2..3 run tag @s add rpg.pa.any
execute if score @s rpg_ps_19 matches 2..3 run tag @s add rpg.pa.any
execute if score @s rpg_ps_18 matches 2..3 run tag @s add rpg.pa.any
execute if score @s rpg_ps_17 matches 2..3 run tag @s add rpg.pa.any
execute if score @s rpg_ps_16 matches 2..3 run tag @s add rpg.pa.any
execute if score @s rpg_ps_15 matches 2..3 run tag @s add rpg.pa.any
execute if score @s rpg_ps_14 matches 2..3 run tag @s add rpg.pa.any
execute if score @s rpg_ps_13 matches 2..3 run tag @s add rpg.pa.any
execute if score @s rpg_ps_12 matches 2..3 run tag @s add rpg.pa.any
execute if score @s rpg_ps_11 matches 2..3 run tag @s add rpg.pa.any
