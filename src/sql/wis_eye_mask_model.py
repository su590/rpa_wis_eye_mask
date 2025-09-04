import dataclasses

@dataclasses.dataclass
class JxFeelFreeToPush:
    live_total_consumption: float = 0.0
    live_total_deal: float = 0.0
    live_total_deal_smart_coupon: float = 0.0
    material_total_click_ratio: float = 0.0
    material_total_transfer_ratio: float = 0.0
    material_total_consumption: float = 0.0
    material_total_consumption_ratio: float = 0.0
    material_total_deal: float = 0.0
    material_total_deal_ratio: float = 0.0
    commodity_total_consumption: float = 0.0
    commodity_user_pay_amount: float = 0.0
    commodity_total_deal_smart_coupon: float = 0.0

@dataclasses.dataclass
class JxNewNine:
    commodity_total_consumption: float = 0.0
    commodity_user_pay_amount: float = 0.0
    commodity_total_deal_smart_coupon: float = 0.0

@dataclasses.dataclass
class WisEyeMaskModel:
    jx_feel_free_to_push: JxFeelFreeToPush = dataclasses.field(default_factory=JxFeelFreeToPush)
    jx_new_nine: JxNewNine = dataclasses.field(default_factory=JxNewNine)
