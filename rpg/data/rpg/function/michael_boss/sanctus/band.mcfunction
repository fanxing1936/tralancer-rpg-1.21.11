$execute as @e[tag=rpg.unit.f,distance=$(lo)..$(hi),tag=!rpg.mkb.sw$(id)] if predicate rpg:michael_boss/grounded run function rpg:michael_boss/sanctus/burn {id:$(id)}
