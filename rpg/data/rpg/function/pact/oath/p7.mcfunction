# 玛门：身无分文就犯禁，每分钟至多一次。
execute if entity @s[level=..4] if score @s rpg_pv_t matches 0 run function rpg:pact/oath/violate
