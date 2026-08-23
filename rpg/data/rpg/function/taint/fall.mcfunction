# 一拍堕落。过半之后一拍两步 —— 越往下掉得越快。
scoreboard players add @s rpg_fall 1
execute if entity @s[scores={rpg_fall=31..}] run scoreboard players add @s rpg_fall 1

# 走满了。return run：不加的话下面还会按最后一档再堆一次攻击。
execute if entity @s[scores={rpg_fall=60..}] at @s run return run function rpg:taint/advent

# 攻击加成整段重写。先摘再挂 —— 同一个 id 挂两次是会叠的。
attribute @s minecraft:attack_damage modifier remove rpg:fall
execute if entity @s[scores={rpg_fall=1..15}] run return run function rpg:taint/f1
execute if entity @s[scores={rpg_fall=16..30}] run return run function rpg:taint/f2
execute if entity @s[scores={rpg_fall=31..45}] run return run function rpg:taint/f3
execute if entity @s[scores={rpg_fall=46..59}] run return run function rpg:taint/f4
