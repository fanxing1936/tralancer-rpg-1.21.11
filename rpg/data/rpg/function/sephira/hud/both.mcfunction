scoreboard players operation #p rpg_sef = @s rpg_mana2
scoreboard players operation #p rpg_sef *= #8 rpg_sef
scoreboard players operation #p rpg_sef /= @s rpg_mana_max
execute if score #p rpg_sef matches 0 run data modify storage rpg:sephira h.n set value {f:"",e:"▱▱▱▱▱▱▱▱"}
execute if score #p rpg_sef matches 1 run data modify storage rpg:sephira h.n set value {f:"▰",e:"▱▱▱▱▱▱▱"}
execute if score #p rpg_sef matches 2 run data modify storage rpg:sephira h.n set value {f:"▰▰",e:"▱▱▱▱▱▱"}
execute if score #p rpg_sef matches 3 run data modify storage rpg:sephira h.n set value {f:"▰▰▰",e:"▱▱▱▱▱"}
execute if score #p rpg_sef matches 4 run data modify storage rpg:sephira h.n set value {f:"▰▰▰▰",e:"▱▱▱▱"}
execute if score #p rpg_sef matches 5 run data modify storage rpg:sephira h.n set value {f:"▰▰▰▰▰",e:"▱▱▱"}
execute if score #p rpg_sef matches 6 run data modify storage rpg:sephira h.n set value {f:"▰▰▰▰▰▰",e:"▱▱"}
execute if score #p rpg_sef matches 7 run data modify storage rpg:sephira h.n set value {f:"▰▰▰▰▰▰▰",e:"▱"}
execute if score #p rpg_sef matches 8.. run data modify storage rpg:sephira h.n set value {f:"▰▰▰▰▰▰▰▰",e:""}
data modify storage rpg:sephira h.mf set from storage rpg:sephira h.m.f
data modify storage rpg:sephira h.me set from storage rpg:sephira h.m.e
data modify storage rpg:sephira h.nf set from storage rpg:sephira h.n.f
data modify storage rpg:sephira h.ne set from storage rpg:sephira h.n.e
function rpg:sephira/hud/both2 with storage rpg:sephira h
