# 空闲时只做一次存在性检查；active 保留 line-major/AoE 掷点语义。
execute if entity @e[tag=rpg.hurt,limit=1] run function rpg:item/sword/off/off_active
