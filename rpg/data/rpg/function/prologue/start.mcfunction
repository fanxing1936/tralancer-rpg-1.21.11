# prologue_multi hub
# 管理员：把执行位置 16 格内最多 4 名玩家立刻编成一组送进序章（有空闲战场时）
tag @a[distance=..16,gamemode=!spectator,tag=!rpg.pr,limit=4,sort=nearest] add rpg.pr.q
scoreboard players set @a[tag=rpg.pr.q,distance=..16] rpg_pr_qt 60
function rpg:prologue/queue
