# 收场 6：清实体、放开区块
execute in rpg:daath positioned 3072.5 64 0.5 run function rpg:daath_fight/slot/sweep
execute in rpg:daath run forceload remove 3040 -32 3104 32
bossbar set rpg:daath_6 players
bossbar set rpg:daath_6 visible false
scoreboard players set #b6 rpg_dt 0
data remove storage rpg:daath s6
