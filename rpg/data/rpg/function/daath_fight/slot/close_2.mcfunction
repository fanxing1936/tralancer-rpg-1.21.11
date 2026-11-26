# 收场 2：清实体、放开区块
execute in rpg:daath positioned 1024.5 64 0.5 run function rpg:daath_fight/slot/sweep
execute in rpg:daath run forceload remove 992 -32 1056 32
bossbar set rpg:daath_2 players
bossbar set rpg:daath_2 visible false
scoreboard players set #b2 rpg_dt 0
data remove storage rpg:daath s2
