export interface BoardSpace {
  id: number;
  name: string;
  monument: string;
  city: string;
  state: string;
  type: "property" | "transport" | "utility" | "chance" | "community" | "tax" | "go" | "jail" | "free_parking" | "go_to_jail";
  color_group?: string;
  price: number;
  base_rent: number;
  rent_1_house: number;
  rent_2_house: number;
  rent_3_house: number;
  rent_4_house: number;
  rent_hotel: number;
  house_cost: number;
  hotel_cost: number;
  mortgage_value: number;
  description: string;
  icon: string;
}

export interface Player {
  id: string;
  name: string;
  token: string;
  color: string;
  cash: number;
  position: number;
  in_jail: boolean;
  jail_turns: number;
  get_out_of_jail_cards: number;
  is_bankrupt: boolean;
  is_bot: boolean;
  bot_profile?: string;
  connected: boolean;
}

export interface PropertyOwnership {
  space_id: number;
  owner_id: string;
  bhavans: number;
  has_mahal: boolean;
  is_mortgaged: boolean;
}

export interface AuctionState {
  space_id: number;
  current_bid: number;
  highest_bidder_id?: string;
  active_bidders: string[];
  expires_at: number;
}

export interface GameLog {
  id: string;
  timestamp: number;
  message: string;
  player_id?: string;
  log_type: "info" | "cash" | "property" | "dice" | "card" | "jail" | "alert";
}

export interface GameCard {
  id: string;
  deck: "chance" | "community";
  title: string;
  description: string;
  action_type: string;
  value?: number;
  house_fee?: number;
  hotel_fee?: number;
}

export interface GameState {
  room_id: string;
  room_code: string;
  host_id: string;
  status: "lobby" | "playing" | "completed";
  players: Player[];
  current_player_index: number;
  dice_1: number;
  dice_2: number;
  doubles_count: number;
  turn_phase: "pre_roll" | "rolled" | "buy_or_auction_decision" | "auction_in_progress" | "card_drawn" | "in_jail_decision" | "pay_rent_due" | "post_turn" | "game_over";
  properties: Record<number, PropertyOwnership>;
  bank_houses: number;
  bank_hotels: number;
  logs: GameLog[];
  active_auction?: AuctionState;
  last_drawn_card?: GameCard;
  winner_id?: string;
  turn_number: number;
}

export interface PlayerTokenInfo {
  id: string;
  name: string;
  finish: string;
  icon: string;
  color: string;
}
