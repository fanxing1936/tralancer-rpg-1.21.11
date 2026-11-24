# rpg:hud/status 调用（as 玩家）
scoreboard players set @s rpg_hud_on 1
data modify storage rpg:sephira h set value {lead:"　",a:"",an:0}
execute if data storage rpg:hud {a:'{"text":""}'} run data modify storage rpg:sephira h.lead set value ""
scoreboard players operation #p rpg_sef = @s rpg_mana
scoreboard players operation #p rpg_sef *= #8 rpg_sef
scoreboard players operation #p rpg_sef /= @s rpg_mana_max
execute if score #p rpg_sef matches 0 run data modify storage rpg:sephira h.m set value {f:"",e:"▱▱▱▱▱▱▱▱"}
execute if score #p rpg_sef matches 1 run data modify storage rpg:sephira h.m set value {f:"▰",e:"▱▱▱▱▱▱▱"}
execute if score #p rpg_sef matches 2 run data modify storage rpg:sephira h.m set value {f:"▰▰",e:"▱▱▱▱▱▱"}
execute if score #p rpg_sef matches 3 run data modify storage rpg:sephira h.m set value {f:"▰▰▰",e:"▱▱▱▱▱"}
execute if score #p rpg_sef matches 4 run data modify storage rpg:sephira h.m set value {f:"▰▰▰▰",e:"▱▱▱▱"}
execute if score #p rpg_sef matches 5 run data modify storage rpg:sephira h.m set value {f:"▰▰▰▰▰",e:"▱▱▱"}
execute if score #p rpg_sef matches 6 run data modify storage rpg:sephira h.m set value {f:"▰▰▰▰▰▰",e:"▱▱"}
execute if score #p rpg_sef matches 7 run data modify storage rpg:sephira h.m set value {f:"▰▰▰▰▰▰▰",e:"▱"}
execute if score #p rpg_sef matches 8.. run data modify storage rpg:sephira h.m set value {f:"▰▰▰▰▰▰▰▰",e:""}
execute if score @s rpg_force matches 1 run function rpg:sephira/hud/holy
execute if score @s rpg_force matches 2 run function rpg:sephira/hud/mana
execute if score @s rpg_force matches 3 run function rpg:sephira/hud/both
