# 名牌（as 精英，storage t 已有 key）
execute if score @s rpg_el_a1 matches 1 run data merge storage rpg:elite {t:{n1:"",c1:"#62D9E8"}}
execute if score @s rpg_el_a2 matches 1 run data merge storage rpg:elite {t:{n2:"",c2:"#62D9E8"}}
execute if score @s rpg_el_a1 matches 2 run data merge storage rpg:elite {t:{n1:"",c1:"#D0D0D0"}}
execute if score @s rpg_el_a2 matches 2 run data merge storage rpg:elite {t:{n2:"",c2:"#D0D0D0"}}
execute if score @s rpg_el_a1 matches 3 run data merge storage rpg:elite {t:{n1:"",c1:"#FF6B5E"}}
execute if score @s rpg_el_a2 matches 3 run data merge storage rpg:elite {t:{n2:"",c2:"#FF6B5E"}}
execute if score @s rpg_el_a1 matches 4 run data merge storage rpg:elite {t:{n1:"",c1:"#D97AD9"}}
execute if score @s rpg_el_a2 matches 4 run data merge storage rpg:elite {t:{n2:"",c2:"#D97AD9"}}
execute if score @s rpg_el_a1 matches 5 run data merge storage rpg:elite {t:{n1:"",c1:"#E8F4FF"}}
execute if score @s rpg_el_a2 matches 5 run data merge storage rpg:elite {t:{n2:"",c2:"#E8F4FF"}}
execute if score @s rpg_el_a1 matches 6 run data merge storage rpg:elite {t:{n1:"",c1:"#70DB70"}}
execute if score @s rpg_el_a2 matches 6 run data merge storage rpg:elite {t:{n2:"",c2:"#70DB70"}}
execute if score @s rpg_el_a1 matches 7 run data merge storage rpg:elite {t:{n1:"",c1:"#FFA25C"}}
execute if score @s rpg_el_a2 matches 7 run data merge storage rpg:elite {t:{n2:"",c2:"#FFA25C"}}
execute if score @s rpg_el_a1 matches 8 run data merge storage rpg:elite {t:{n1:"",c1:"#A276BE"}}
execute if score @s rpg_el_a2 matches 8 run data merge storage rpg:elite {t:{n2:"",c2:"#A276BE"}}
execute if score @s rpg_el_a1 matches 9 run data merge storage rpg:elite {t:{n1:"",c1:"#C77298"}}
execute if score @s rpg_el_a2 matches 9 run data merge storage rpg:elite {t:{n2:"",c2:"#C77298"}}
execute if score @s rpg_el_a1 matches 10 run data merge storage rpg:elite {t:{n1:"",c1:"#FFD85A"}}
execute if score @s rpg_el_a2 matches 10 run data merge storage rpg:elite {t:{n2:"",c2:"#FFD85A"}}
execute unless entity @s[tag=rpg.el.boss] run return run function rpg:elite/name1 with storage rpg:elite t
function rpg:elite/name2 with storage rpg:elite t
