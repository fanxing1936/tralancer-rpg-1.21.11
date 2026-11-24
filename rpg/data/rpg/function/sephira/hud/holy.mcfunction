scoreboard players operation #p rpg_sef = @s rpg_vital
scoreboard players operation #p rpg_sef *= #8 rpg_sef
scoreboard players operation #p rpg_sef /= #100 rpg_sef
execute if score #p rpg_sef matches 0 run data modify storage rpg:sephira h.v set value {f:"",e:"▱▱▱▱▱▱▱▱"}
execute if score #p rpg_sef matches 1 run data modify storage rpg:sephira h.v set value {f:"▰",e:"▱▱▱▱▱▱▱"}
execute if score #p rpg_sef matches 2 run data modify storage rpg:sephira h.v set value {f:"▰▰",e:"▱▱▱▱▱▱"}
execute if score #p rpg_sef matches 3 run data modify storage rpg:sephira h.v set value {f:"▰▰▰",e:"▱▱▱▱▱"}
execute if score #p rpg_sef matches 4 run data modify storage rpg:sephira h.v set value {f:"▰▰▰▰",e:"▱▱▱▱"}
execute if score #p rpg_sef matches 5 run data modify storage rpg:sephira h.v set value {f:"▰▰▰▰▰",e:"▱▱▱"}
execute if score #p rpg_sef matches 6 run data modify storage rpg:sephira h.v set value {f:"▰▰▰▰▰▰",e:"▱▱"}
execute if score #p rpg_sef matches 7 run data modify storage rpg:sephira h.v set value {f:"▰▰▰▰▰▰▰",e:"▱"}
execute if score #p rpg_sef matches 8.. run data modify storage rpg:sephira h.v set value {f:"▰▰▰▰▰▰▰▰",e:""}
execute store result storage rpg:sephira h.an int 1 run scoreboard players get @s rpg_assim
execute if score @s rpg_assim matches 1.. run function rpg:sephira/hud/holy_a with storage rpg:sephira h
execute unless score @s rpg_assim matches 1.. run function rpg:sephira/hud/holy_m with storage rpg:sephira h
