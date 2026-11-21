# 武器名前的源图标：名字被包成 [图标, 空格, 原名]，ng:1b 记着包过。每次渲染先拆再按当前的源重包。
execute if data entity @e[type=minecraft:item_display,tag=rpg.fg.ws,limit=1] item.components."minecraft:custom_data".rpg_eq{ng:1b} run function rpg:forge/name/unwrap
execute if data storage rpg:forge e{src:"none"} run return 0
execute unless data entity @e[type=minecraft:item_display,tag=rpg.fg.ws,limit=1] item.components."minecraft:custom_name" run return 0
execute if data storage rpg:forge e{src:"faith"} run function rpg:forge/name/wrap {g:""}
execute if data storage rpg:forge e{src:"hope"} run function rpg:forge/name/wrap {g:""}
execute if data storage rpg:forge e{src:"resolve"} run function rpg:forge/name/wrap {g:""}
execute if data storage rpg:forge e{src:"malice"} run function rpg:forge/name/wrap {g:""}
execute if data storage rpg:forge e{src:"hatred"} run function rpg:forge/name/wrap {g:""}
execute if data storage rpg:forge e{src:"pride"} run function rpg:forge/name/wrap {g:""}
