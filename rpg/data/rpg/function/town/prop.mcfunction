# 地下城道具（add_town_models.py 的 rpg:town_models/prop/<名>；构建时还没有的就不放）
$data modify storage rpg:town pn set value "$(n)"
execute if data storage rpg:town {pn:"pyre"} run function rpg:town_models/prop/pyre
execute if data storage rpg:town {pn:"cage"} run function rpg:town_models/prop/cage
execute if data storage rpg:town {pn:"grave_a"} run function rpg:town_models/prop/grave_a
execute if data storage rpg:town {pn:"grave_b"} run function rpg:town_models/prop/grave_b
execute if data storage rpg:town {pn:"candles_a"} run function rpg:town_models/prop/candles_a
execute if data storage rpg:town {pn:"candles_b"} run function rpg:town_models/prop/candles_b
execute if data storage rpg:town {pn:"cauldron"} run function rpg:town_models/prop/cauldron
execute if data storage rpg:town {pn:"bell"} run function rpg:town_models/prop/bell
execute if data storage rpg:town {pn:"barrel"} run function rpg:town_models/prop/barrel
execute if data storage rpg:town {pn:"crate"} run function rpg:town_models/prop/crate
execute if data storage rpg:town {pn:"crate_pile"} run function rpg:town_models/prop/crate_pile
execute if data storage rpg:town {pn:"cart"} run function rpg:town_models/prop/cart
