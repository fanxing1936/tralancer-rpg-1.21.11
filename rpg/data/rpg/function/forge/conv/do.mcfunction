# 材料转换：60 打开，61..64 换一次
execute if score #do rpg_fg matches 60 run return run function rpg:forge/conv/open
execute if score #do rpg_fg matches 61 run return run function rpg:forge/conv/r61
execute if score #do rpg_fg matches 62 run return run function rpg:forge/conv/r62
execute if score #do rpg_fg matches 63 run return run function rpg:forge/conv/r63
execute if score #do rpg_fg matches 64 run return run function rpg:forge/conv/r64
execute if score #do rpg_fg matches 65 run return run function rpg:forge/bp/frag_open
