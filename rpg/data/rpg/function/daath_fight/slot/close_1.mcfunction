# 收场 1：清实体、放开区块
execute in rpg:daath positioned 512.5 64 0.5 run function rpg:daath_fight/slot/sweep
execute in rpg:daath run forceload remove 480 -32 544 32
bossbar set rpg:daath_1 players
bossbar set rpg:daath_1 visible false
scoreboard players set #b1 rpg_dt 0
data remove storage rpg:daath s1
