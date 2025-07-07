package com.eva.EvaSupportAgent.product.vo;

import java.math.BigDecimal;
import java.util.Date;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@AllArgsConstructor
@NoArgsConstructor
public class OrderHistoryVO {

    private Long id;
    private Long userId;
    private Long productId;
    private int quantity;
    private BigDecimal price;
    private String status;
    private String productName;
    private String productImage;
    private Date orderedAt;

    // Getters and Setters
}

