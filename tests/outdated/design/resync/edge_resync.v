
module edge_resync #(
	parameter DEPTH = 2, // number of DFF (MTBF)
	parameter EDGE  = 0 // 0: rising edge, 1: falling edge, 2: both
) (
	// clock signals
	input  wire clk,
	// reset signals
	input  wire rstb,
	// signal transfer
	input  wire sig,
	output wire sig_r
);

	reg [DEPTH-1:0] i;

	// resync in the other clock domain
	always @(posedge clk or negedge rstb)
	begin
		if(!rstb)
			i <= {DEPTH{1'b0}};
		else
			i <= {i[DEPTH-2:0], sig};
	end

	// edge
	if (EDGE == 0)
		assign sig_r = ~i[DEPTH-1] &  i[DEPTH-2];
	else if (EDGE == 1)
		assign sig_r =  i[DEPTH-1] & ~i[DEPTH-2];
	else
		assign sig_r =  i[DEPTH-1] ^  i[DEPTH-2];

endmodule