# 每 2 秒：配方书里出现原版配方（捡东西时原版会自动解锁）就整个收回。
# recipe_unlocked 进度在 1.21.11 必须指定配方，没法当「任意解锁」用，所以改成轮询。
scoreboard players add #t rpg_wl_rl 1
execute if score #t rpg_wl_rl matches 40.. run function rpg:world/recipe_scan
