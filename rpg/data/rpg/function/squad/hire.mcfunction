# 募兵旗 —— 由 rpg:item/squad_hire 在长按右键时触发。
#
# 两步：身边没有待雇者就先招一个来（不花钱），有待雇者才是真的雇佣。
# 「只有对未雇佣的佣兵才会雇佣」——雇的是**眼前这个人**，不是凭空变一个出来。
advancement revoke @s only rpg:item/squad_hire
execute if entity @s[scores={rpg_sq_t=1..}] run return 0
scoreboard players set @s rpg_sq_t 10

# 头一次募兵先领一个队伍编号。多人下认人全靠它，不靠"最近的玩家"。
execute unless score @s rpg_squad = @s rpg_squad run function rpg:squad/enroll
scoreboard players operation #sq rpg_squad = @s rpg_squad

# 潜行 = 给身边的在编佣兵升一级（原本这个组合是空着的）
execute if predicate rpg:sneaking run return run function rpg:squad/upgrade

execute if entity @e[type=minecraft:husk,tag=rpg.sq.free,distance=..6,limit=1] run return run function rpg:squad/enlist
function rpg:squad/post
