# 记下回程位置、游戏模式、经验，存背包（as 玩家，宏参数 id）
$data modify storage rpg:pr_i1 r.p$(id).dim set from entity @s Dimension
$execute store result storage rpg:pr_i1 r.p$(id).x double 0.01 run data get entity @s Pos[0] 100
$execute store result storage rpg:pr_i1 r.p$(id).y double 0.01 run data get entity @s Pos[1] 100
$execute store result storage rpg:pr_i1 r.p$(id).z double 0.01 run data get entity @s Pos[2] 100
$execute store result storage rpg:pr_i1 r.p$(id).yaw float 0.01 run data get entity @s Rotation[0] 100
$execute store result storage rpg:pr_i1 r.p$(id).xl int 1 run experience query @s levels
$execute store result storage rpg:pr_i1 r.p$(id).xp int 1 run experience query @s points
$data modify storage rpg:pr_i1 r.p$(id).gm set value "survival"
$execute if entity @s[gamemode=creative] run data modify storage rpg:pr_i1 r.p$(id).gm set value "creative"
$execute if entity @s[gamemode=adventure] run data modify storage rpg:pr_i1 r.p$(id).gm set value "adventure"
$execute if entity @s[gamemode=spectator] run data modify storage rpg:pr_i1 r.p$(id).gm set value "spectator"
