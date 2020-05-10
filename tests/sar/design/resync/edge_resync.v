
module edge_resync #(
	parameter DEPTH = 2, // number of DFF (MTBF)
	parameter EDGE  = 0 // 0: rising edge, 1: falling edge, 2: both
) (
	// clock signals
	input  wire CK,
	// reset signals
	input  wire RB,
	// signal transfer
	input  wire A,
	output wire Q
);

	reg [DEPTH-1:0] i;

	// resync in the other clock domain
	always @(posedge CK or negedge RB)
	begin
		if(!RB)
			i <= {DEPTH{1'b0}};
		else
			i <= {i[DEPTH-2:0], A};
	end

	// edge
	if (EDGE == 0)
		assign Q = ~i[DEPTH-1] &  i[DEPTH-2];
	else if (EDGE == 1)
		assign Q =  i[DEPTH-1] & ~i[DEPTH-2];
	else
		assign Q =  i[DEPTH-1] ^  i[DEPTH-2];

endmodule