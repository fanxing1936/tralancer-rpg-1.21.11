# 收场 9：清实体、放开区块
execute in rpg:daath positioned 4608.5 64 0.5 run function rpg:daath_fight/slot/sweep
execute in rpg:daath run forceload remove 4576 -32 4640 32
bossbar set rpg:daath_9 players
bossbar set rpg:daath_9 visible false
scoreboard players set #b9 rpg_dt 0
data remove storage rpg:daath s9
