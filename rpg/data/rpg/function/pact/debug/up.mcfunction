# 直接升一阶，不要材料也不要击败领主。
execute if score @s rpg_pact_lv matches 3.. run return 0
function rpg:pact/up_done
