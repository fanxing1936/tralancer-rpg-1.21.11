# 别西卜：饿着就犯禁，每分钟至多一次。
execute if score @s rpg_ps_food matches ..5 if score @s rpg_pv_t matches 0 run function rpg:pact/oath/violate
