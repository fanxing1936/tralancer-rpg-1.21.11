# 每个特效实体每刻（as/at 它）。
scoreboard players remove @s rpg_mk_life 1
execute if score @s rpg_mk_life matches ..0 run return run kill @s
execute if entity @s[tag=rpg.mkb.walker] run return run function rpg:michael_boss/fx/walker
execute if entity @s[tag=rpg.mkb.feather] run return run function rpg:michael_boss/fx/feather
execute if entity @s[tag=rpg.mkb.trail] run return run function rpg:michael_boss/fx/trail
execute if entity @s[tag=rpg.mkb.rainf] run return run function rpg:michael_boss/fx/rainf
execute if entity @s[tag=rpg.mkb.rainfeather] run return run function rpg:michael_boss/fx/rainfeather
execute if entity @s[tag=rpg.mkb.spoke] run return run function rpg:michael_boss/fx/spoke
execute if entity @s[tag=rpg.mkb.wave] run return run function rpg:michael_boss/fx/wave
execute if entity @s[tag=rpg.mkb.orb] run return run function rpg:michael_boss/fx/orb
execute if entity @s[tag=rpg.mkb.trump] run return run function rpg:michael_boss/fx/trump
execute if entity @s[tag=rpg.mkb.meteor] run return run function rpg:michael_boss/fx/meteor
execute if entity @s[tag=rpg.mkb.bigstar] run return run function rpg:michael_boss/fx/bigstar
execute if score @s rpg_mk_kd matches 1.. run function rpg:michael_boss/fx/kind
