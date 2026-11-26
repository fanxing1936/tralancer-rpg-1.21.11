execute if score @s rpg_dt_t matches 1 run execute facing entity @p[tag=rpg.dt.me] feet rotated ~ 0 run rotate @s ~ ~
execute if score @s rpg_dt_t matches 8 run execute positioned ^-5 ^ ^6 run function rpg:daath_fight/pact/mark
execute if score @s rpg_dt_t matches 8 run execute positioned ^0 ^ ^4 run function rpg:daath_fight/pact/mark
execute if score @s rpg_dt_t matches 8 run execute positioned ^5 ^ ^6 run function rpg:daath_fight/pact/mark
execute if score @s rpg_dt_t matches 28 run execute positioned ^-5 ^ ^6 run function rpg:daath_fight/pact/pillar
execute if score @s rpg_dt_t matches 28 run execute positioned ^0 ^ ^4 run function rpg:daath_fight/pact/pillar
execute if score @s rpg_dt_t matches 28 run execute positioned ^5 ^ ^6 run function rpg:daath_fight/pact/pillar
execute if score @s rpg_dt_t matches 48.. run function rpg:daath_fight/sk/end
