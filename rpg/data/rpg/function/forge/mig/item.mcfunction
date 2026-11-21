# 旧系统留下的东西：12 行旧属性块、等级、镀金、旧符文符石、旧分支烙印。
scoreboard players set #mlv rpg_fg 1
scoreboard players set #mgild rpg_fg 0
scoreboard players set #mstrip rpg_fg 0
scoreboard players set #mrestore rpg_fg 0
scoreboard players set #mname rpg_fg 0
data remove storage rpg:forge mig
data modify storage rpg:forge mig.refund set value []
data remove storage rpg:forge t
data modify storage rpg:forge t.a set from entity @e[type=minecraft:item_display,tag=rpg.fg.ws,limit=1] item.components."minecraft:lore"[0]
data modify storage rpg:forge t.b set from entity @e[type=minecraft:item_display,tag=rpg.fg.ws,limit=1] item.components."minecraft:lore"[5]
execute if data storage rpg:forge t{b:{extra:[{text:"[已镀金]"}]}} run scoreboard players set #mgild rpg_fg 1
execute if data storage rpg:forge t{a:{extra:[{text:"+------装备属性------+"}]}} run function rpg:forge/mig/old_block
execute if data entity @e[type=minecraft:item_display,tag=rpg.fg.ws,limit=1] item.components."minecraft:custom_data".level store result score #mlv rpg_fg run data get entity @e[type=minecraft:item_display,tag=rpg.fg.ws,limit=1] item.components."minecraft:custom_data".level
execute if score #mlv rpg_fg matches 11.. run scoreboard players set #mlv rpg_fg 10
execute if score #mlv rpg_fg matches ..0 run scoreboard players set #mlv rpg_fg 1
data remove entity @e[type=minecraft:item_display,tag=rpg.fg.ws,limit=1] item.components."minecraft:custom_data".weapon_tag
data remove entity @e[type=minecraft:item_display,tag=rpg.fg.ws,limit=1] item.components."minecraft:custom_data".level
data remove entity @e[type=minecraft:item_display,tag=rpg.fg.ws,limit=1] item.components."minecraft:custom_data".exp
data remove entity @e[type=minecraft:item_display,tag=rpg.fg.ws,limit=1] item.components."minecraft:custom_data".exp_max
data remove entity @e[type=minecraft:item_display,tag=rpg.fg.ws,limit=1] item.components."minecraft:custom_data".xilian
data remove entity @e[type=minecraft:item_display,tag=rpg.fg.ws,limit=1] item.components."minecraft:custom_data".add_weapon_tag
execute if data entity @e[type=minecraft:item_display,tag=rpg.fg.ws,limit=1] item.components."minecraft:custom_data".absorption_tag run function rpg:forge/mig/r_absorption_tag
execute if data entity @e[type=minecraft:item_display,tag=rpg.fg.ws,limit=1] item.components."minecraft:custom_data".blow_tag run function rpg:forge/mig/r_blow_tag
execute if data entity @e[type=minecraft:item_display,tag=rpg.fg.ws,limit=1] item.components."minecraft:custom_data".boom_tag run function rpg:forge/mig/r_boom_tag
execute if data entity @e[type=minecraft:item_display,tag=rpg.fg.ws,limit=1] item.components."minecraft:custom_data".damage_tag run function rpg:forge/mig/r_damage_tag
execute if data entity @e[type=minecraft:item_display,tag=rpg.fg.ws,limit=1] item.components."minecraft:custom_data".dark_tag run function rpg:forge/mig/r_dark_tag
execute if data entity @e[type=minecraft:item_display,tag=rpg.fg.ws,limit=1] item.components."minecraft:custom_data".deep_tag run function rpg:forge/mig/r_deep_tag
execute if data entity @e[type=minecraft:item_display,tag=rpg.fg.ws,limit=1] item.components."minecraft:custom_data".ebb_tag run function rpg:forge/mig/r_ebb_tag
execute if data entity @e[type=minecraft:item_display,tag=rpg.fg.ws,limit=1] item.components."minecraft:custom_data".health_tag run function rpg:forge/mig/r_health_tag
execute if data entity @e[type=minecraft:item_display,tag=rpg.fg.ws,limit=1] item.components."minecraft:custom_data".ink_tag run function rpg:forge/mig/r_ink_tag
execute if data entity @e[type=minecraft:item_display,tag=rpg.fg.ws,limit=1] item.components."minecraft:custom_data".pin_tag run function rpg:forge/mig/r_pin_tag
execute if data entity @e[type=minecraft:item_display,tag=rpg.fg.ws,limit=1] item.components."minecraft:custom_data".projectiles_tag run function rpg:forge/mig/r_projectiles_tag
execute if data entity @e[type=minecraft:item_display,tag=rpg.fg.ws,limit=1] item.components."minecraft:custom_data".sunder_tag run function rpg:forge/mig/r_sunder_tag
execute if data entity @e[type=minecraft:item_display,tag=rpg.fg.ws,limit=1] item.components."minecraft:custom_data".wilt_tag run function rpg:forge/mig/r_wilt_tag
execute if data entity @e[type=minecraft:item_display,tag=rpg.fg.ws,limit=1] item.components."minecraft:custom_data".flame_tag run function rpg:forge/mig/s_flame_tag
execute if data entity @e[type=minecraft:item_display,tag=rpg.fg.ws,limit=1] item.components."minecraft:custom_data".quake_tag run function rpg:forge/mig/s_quake_tag
execute if data entity @e[type=minecraft:item_display,tag=rpg.fg.ws,limit=1] item.components."minecraft:custom_data".shade_tag run function rpg:forge/mig/s_shade_tag
execute if data entity @e[type=minecraft:item_display,tag=rpg.fg.ws,limit=1] item.components."minecraft:custom_data".sweep_tag run function rpg:forge/mig/s_sweep_tag
execute if data entity @e[type=minecraft:item_display,tag=rpg.fg.ws,limit=1] item.components."minecraft:custom_data".tide_tag run function rpg:forge/mig/s_tide_tag
execute if data entity @e[type=minecraft:item_display,tag=rpg.fg.ws,limit=1] item.components."minecraft:custom_data".wind_tag run function rpg:forge/mig/s_wind_tag
function rpg:forge/mig/strip
execute if score #mrestore rpg_fg matches 1 run function rpg:forge/mig/restore_use
scoreboard players set #nat rpg_fg 0
execute if data entity @e[type=minecraft:item_display,tag=rpg.fg.ws,limit=1] item.components."minecraft:custom_data".michael_rib_tag run scoreboard players set #nat rpg_fg 1
execute if data entity @e[type=minecraft:item_display,tag=rpg.fg.ws,limit=1] item.components."minecraft:custom_data".michael_spine_tag run scoreboard players set #nat rpg_fg 1
execute if data entity @e[type=minecraft:item_display,tag=rpg.fg.ws,limit=1] item.components."minecraft:custom_data".power_tag run scoreboard players set #nat rpg_fg 1
execute if data entity @e[type=minecraft:item_display,tag=rpg.fg.ws,limit=1] item.components."minecraft:custom_data"{armor_set:"holy"} run scoreboard players set #nat rpg_fg 1
execute if data entity @e[type=minecraft:item_display,tag=rpg.fg.ws,limit=1] item.components."minecraft:custom_data"{holy_weapon_tag:2b} run function rpg:forge/mig/brand {src:"hope",key:"holy_weapon_tag"}
execute if data entity @e[type=minecraft:item_display,tag=rpg.fg.ws,limit=1] item.components."minecraft:custom_data"{holy_weapon_tag:3b} run function rpg:forge/mig/brand {src:"resolve",key:"holy_weapon_tag"}
execute if score #nat rpg_fg matches 0 if data entity @e[type=minecraft:item_display,tag=rpg.fg.ws,limit=1] item.components."minecraft:custom_data"{holy_weapon_tag:1b} run function rpg:forge/mig/brand {src:"faith",key:"holy_weapon_tag"}
execute if data entity @e[type=minecraft:item_display,tag=rpg.fg.ws,limit=1] item.components."minecraft:custom_data"{devil_weapon_tag:1b} run function rpg:forge/mig/brand {src:"malice",key:"devil_weapon_tag"}
execute if data entity @e[type=minecraft:item_display,tag=rpg.fg.ws,limit=1] item.components."minecraft:custom_data"{devil_weapon_tag:2b} run function rpg:forge/mig/brand {src:"hatred",key:"devil_weapon_tag"}
execute if data entity @e[type=minecraft:item_display,tag=rpg.fg.ws,limit=1] item.components."minecraft:custom_data"{devil_weapon_tag:3b} run function rpg:forge/mig/brand {src:"pride",key:"devil_weapon_tag"}
execute if score #mname rpg_fg matches 1 run function rpg:forge/mig/restore_name
