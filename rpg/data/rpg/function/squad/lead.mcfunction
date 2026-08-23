# 以雇主的身份跑一遍自己的队伍。
#
# 临时挂 rpg.sq.boss：命令执行是单线程的，同一刻只可能有一个玩家挂着它，
# 所以队员那边的 @a[tag=rpg.sq.boss,limit=1] 是**精确的**，
# 而不是"碰巧最近的那个玩家"。多人下这一点是全部归属逻辑的地基。
tag @s add rpg.sq.boss
scoreboard players operation #sq rpg_squad = @s rpg_squad

# 本队当前的攻击目标，标出来给队员用（同样只在这一段里存活）
scoreboard players set #mark rpg_squad 0
execute as @e[tag=rpg.sq.aim,distance=..64] if score @s rpg_sq_aim = #sq rpg_squad run function rpg:squad/set_mark

# 搜索半径必须**大于**归队距离：否则掉出 LEASH 的人连这一层都进不来，
# 那条"太远就拉回来"永远轮不到他 —— 人就永久丢了。
execute as @e[type=minecraft:husk,tag=rpg.squad,distance=..128] if score @s rpg_squad = #sq rpg_squad at @s run function rpg:squad/member

tag @e[tag=rpg.sq.mark] remove rpg.sq.mark
tag @s remove rpg.sq.boss
