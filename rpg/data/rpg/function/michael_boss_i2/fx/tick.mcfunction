# 每个特效实体每刻（as/at 它）。
scoreboard players remove @s rpg_mk_life 1
execute if score @s rpg_mk_life matches ..0 run return run kill @s
execute if entity @s[tag=rpg.mkb.walker] run return run function rpg:michael_boss_i2/fx/walker
execute if entity @s[tag=rpg.mkb.feather] run return run function rpg:michael_boss_i2/fx/feather
execute if entity @s[tag=rpg.mkb.trail] run return run function rpg:michael_boss_i2/fx/trail
execute if entity @s[tag=rpg.mkb.rainf] run return run function rpg:michael_boss_i2/fx/rainf
execute if entity @s[tag=rpg.mkb.rainfeather] run return run function rpg:michael_boss_i2/fx/rainfeather
execute if entity @s[tag=rpg.mkb.spoke] run return run function rpg:michael_boss_i2/fx/spoke
execute if entity @s[tag=rpg.mkb.wave] run return run function rpg:michael_boss_i2/fx/wave
execute if entity @s[tag=rpg.mkb.orb] run return run function rpg:michael_boss_i2/fx/orb
execute if entity @s[tag=rpg.mkb.trump] run return run function rpg:michael_boss_i2/fx/trump
execute if entity @s[tag=rpg.mkb.meteor] run return run function rpg:michael_boss_i2/fx/meteor
execute if entity @s[tag=rpg.mkb.bigstar] run return run function rpg:michael_boss_i2/fx/bigstar
execute if score @s rpg_mk_kd matches 1.. run function rpg:michael_boss_i2/fx/kind
