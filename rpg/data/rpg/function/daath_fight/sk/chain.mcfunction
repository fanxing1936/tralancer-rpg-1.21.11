# 起手十刻，之后一下接一下
execute if score @s rpg_dt_t < @s rpg_dt_ht run function rpg:daath_fight/chain/close
execute if score @s rpg_dt_t = @s rpg_dt_ht run function rpg:daath_fight/chain/strike
execute if score @s rpg_dt_t >= @s rpg_dt_ln run function rpg:daath_fight/chain/next
