package com.eva.EvaSupportAgent.product.model;

import java.math.BigDecimal;
import java.util.Date;

import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.Table;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Entity
@Table(name="product_order_history")
@Data
@AllArgsConstructor
@NoArgsConstructor
public class OrderHistory {

	@Id
	@GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    private Long userId;
    private Long productId;
    private int quantity;
    private BigDecimal price;
    private String status;
    private String productName;
    private Date orderedOn;
    
}
