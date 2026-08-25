# 罪约蓄势期间由恶魔自己的计时器推进，多只同时存在也互不覆盖。
function rpg:taint/ult_charge
scoreboard players remove @s rpg_dm_ult 1
execute if entity @s[scores={rpg_dm_ult=..0}] run function rpg:taint/ult_resolve
