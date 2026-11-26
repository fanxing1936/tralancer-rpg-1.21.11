# 收场 8：清实体、放开区块
execute in rpg:daath positioned 4096.5 64 0.5 run function rpg:daath_fight/slot/sweep
execute in rpg:daath run forceload remove 4064 -32 4128 32
bossbar set rpg:daath_8 players
bossbar set rpg:daath_8 visible false
scoreboard players set #b8 rpg_dt 0
data remove storage rpg:daath s8
