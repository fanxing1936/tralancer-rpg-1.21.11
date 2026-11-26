# 收场 3：清实体、放开区块
execute in rpg:daath positioned 1536.5 64 0.5 run function rpg:daath_fight/slot/sweep
execute in rpg:daath run forceload remove 1504 -32 1568 32
bossbar set rpg:daath_3 players
bossbar set rpg:daath_3 visible false
scoreboard players set #b3 rpg_dt 0
data remove storage rpg:daath s3
